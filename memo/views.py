from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import MemoForm
from .models import Memo


@login_required
def memo_create(request):
    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.author = request.user
            memo.save()
            messages.success(request, '메모가 저장되었습니다!')
            return redirect('memo_list')  # 목록으로 이동
        else:
            messages.error(request, '입력 내용을 확인해 주세요.')
    else:
        form = MemoForm()

    return render(request, 'memo/memo_form.html', {'form': form})
@login_required
def memo_list(request):
    memos = Memo.objects.filter(author=request.user)
    return render(request, 'memo/memo_list.html', {'memos': memos})


@login_required
def memo_detail(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, author=request.user)
    return render(request, 'memo/memo_detail.html', {'memo': memo})
