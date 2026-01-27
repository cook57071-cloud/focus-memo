from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MemoForm
from .models import Memo
from django.contrib import messages

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
