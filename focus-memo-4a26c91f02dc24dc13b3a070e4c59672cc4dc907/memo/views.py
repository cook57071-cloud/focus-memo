from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import MemoForm
from .models import Memo, Category



@login_required
def memo_list(request):
    q = (request.GET.get("q") or "").strip()
    category_id = request.GET.get("category")
    sort = request.GET.get("sort") or "latest"

    memos = Memo.objects.filter(author=request.user).select_related("category")

    if category_id:
        memos = memos.filter(category_id=category_id)

    if q:
        memos = memos.filter(content__icontains=q)

    if sort == "oldest":
        memos = memos.order_by("created_at")
    else:
        memos = memos.order_by("-created_at")

    categories = Category.objects.all().order_by("order", "id")

    return render(request, "memo/memo_list.html", {
        "memos": memos,
        "q": q,
        "categories": categories,
        "selected_category": category_id,
        "sort": sort,
    })



@login_required
def memo_detail(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, author=request.user)
    return render(request, 'memo/memo_detail.html', {'memo': memo})




@login_required
def memo_create(request):
    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.author = request.user
            memo.save()
            messages.success(request, '메모가 저장되었습니다!')
            return redirect('memo:list')
        messages.error(request, '입력 내용을 확인해 주세요.')
    else:
        form = MemoForm()

    # ✅ 무조건 여기(함수 끝, render 직전)
    categories = Category.objects.all().order_by('id')
    return render(request, 'memo/memo_form.html', {'form': form, 'categories': categories})


@login_required
def memo_update(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, author=request.user)

    if request.method == 'POST':
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            messages.success(request, '메모가 수정되었습니다.')
            return redirect('memo:detail', memo_id=memo.id)
        messages.error(request, '입력 내용을 확인해 주세요.')
    else:
        form = MemoForm(instance=memo)

    categories = Category.objects.all().order_by('id')
    return render(request, 'memo/memo_form.html', {'form': form, 'is_update': True, 'categories': categories})




@require_POST
@login_required
def memo_delete(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, author=request.user)
    memo.delete()
    messages.success(request, '메모가 삭제되었습니다.')
    return redirect('memo:list')
