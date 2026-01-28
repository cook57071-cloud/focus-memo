from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MemoForm
from .models import Memo
from django.views.decorators.http import require_POST



@login_required  # 로그인한 사용자만 접근 가능
def memo_create(request):
    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            # 현재 로그인한 유저를 작성자로 지정
            memo.author = request.user
            memo.save()
            messages.success(request, '메모가 저장되었습니다!')
            return redirect('/admin/')  # 임시로 관리자 페이지로
        else:
            messages.error(request, '입력 내용을 확인해 주세요.')
    else:
        form = MemoForm()

    return render(request, 'memo/memo_form.html', {'form': form})

from django.views.decorators.http import require_POST

@require_POST
@login_required
def memo_delete(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, author=request.user)
    memo.delete()
    messages.success(request, "메모가 삭제되었습니다.")
    return redirect('memo_list')

@login_required
def memo_list(request):
    memos = Memo.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'memo/memo_list.html', {'memos': memos})


@login_required
def memo_detail(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, author=request.user)
    return render(request, 'memo/memo_detail.html', {'memo': memo})

@login_required
def memo_update(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, author=request.user)

    if request.method == 'POST':
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            messages.success(request, '메모가 수정되었습니다.')
            return redirect('memo_detail', memo_id=memo.id)
    else:
        form = MemoForm(instance=memo)

    return render(request, 'memo/memo_form.html', {
        'form': form,
        'is_update': True,
    })
