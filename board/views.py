from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

from .models import Board

# 인덱스 뷰 테스트
# def index(request):
#     context = {
#         'title': 'Board list',
#         'board_list': [
#             {'no':1, 'title': '목록1'},
#             {'no':2, 'title': '목록2'},
#             {'no':3, 'title': '목록3'},
#             {'no':4, 'title': '목록4'},
#             {'no':5, 'title': '목록5'},
#         ]
#     }
#     return render(request, 'board/index.html', context)
from django.core.paginator import Paginator

def index(request): #게시글 목록
    all_boards = Board.objects.all().order_by("-pub_date") #모든 데이터 조회, 내침차순(-표시) 조회
    paginator = Paginator(all_boards, 5)  #글을 5개씩 출력
    page = int(request.GET.get('page', 1)) # index로 GET요청이 들어올시 page 파라메타를 읽는다  없는경우 디폴트로 1번째 페이지
    board_list = paginator.get_page(page)

    return render(request, 'board/index.html', {'title':'Board List', 'board_list':all_boards})

def detail(request, board_id): #상세페이지
    board = Board.objects.get(id=board_id)
    return render(request, 'board/detail.html', {'board': board})

def write(request): #글쓰기
    return render(request, 'board/write.html')

def write_board(request): #글을 등록시 submit처리
    b = Board(title=request.POST['title'], content=request.POST['detail'], author="choi", pub_date=timezone.now())
    b.save()
    return HttpResponseRedirect(reverse('board:index'))

def create_reply(request, board_id): #댓글 submit 처리
    b = Board.objects.get(id = board_id)
    b.reply_set.create(comment=request.POST['comment'], rep_date=timezone.now())
    return HttpResponseRedirect(reverse('board:detail', args=(board_id,)))