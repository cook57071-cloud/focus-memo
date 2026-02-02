from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import MemoForm
from .models import Memo, Category



@login_required
def memo_list(request):
    # ✅ 여기 추가 (q/sort/category 먼저 정의)
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "latest")
    selected_category = request.GET.get("category", "")

    memos = Memo.objects.all().select_related("category")

    # 검색
    if q:
        memos = memos.filter(content__icontains=q)

    # 카테고리 필터 (category가 숫자 id로 넘어오는 구조일 때)
    if selected_category:
        memos = memos.filter(category_id=selected_category)

    # 정렬
    if sort == "oldest":
        memos = memos.order_by("created_at")
    else:
        memos = memos.order_by("-created_at")

    categories = Category.objects.all().order_by("order")

    return render(request, "memo/memo_list.html", {
        "memos": memos,
        "categories": categories,
        "selected_category": selected_category,
        "q": q,
        "sort": sort,
    })



@login_required
def memo_detail(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, user=request.user)
    return render(request, 'memo/memo_detail.html', {'memo': memo})




@login_required
def memo_create(request):
    if request.method == 'POST':
        # 1. 폼 데이터 가져오기
        form = MemoForm(request.POST)
        
        # 2. 폼 검증 (여기서 False가 나면 저장이 안 됨)
        if form.is_valid():
            memo = form.save(commit=False)
            
            # [수정 포인트] author가 아니라 user 필드에 저장해야 함!
            memo.user = request.user 
            
            memo.save()
            messages.success(request, '메모가 저장되었습니다!')

@login_required
def memo_update(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, user=request.user)

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
    memo = get_object_or_404(Memo, id=memo_id, user=request.user)
    memo.delete()
    messages.success(request, '메모가 삭제되었습니다.')
    return redirect('memo:list')
