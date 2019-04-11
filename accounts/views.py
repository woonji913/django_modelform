from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm #UserChangeForm #UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash # 비번 변경 시에도 로그인 유지
from django.contrib.auth import get_user_model as User
from django.contrib.auth.decorators import login_required
from .forms import UserCustomChangeForm, UserCustomCreationForm


# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
        
    if request.method == 'POST':
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()         #1
            auth_login(request, user)  #2
            return redirect('boards:index')
    else:
        form = UserCustomCreationForm()
    context = {'form':form}
    return render(request, 'accounts/auth_form.html', context)
    
def login(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.POST.get('next') or 'boards:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
        'next': request.GET.get('next',''),
    }
    return render(request, 'accounts/login.html', context)
        
def logout(request):
    auth_logout(request)
    return redirect('boards:index')
    
def delete(request):
    user = request.user
    if request.method == "POST":
        # DELETE
        user.delete()
    return redirect('boards:index')
    
def edit(request):
    if request.method == 'POST':
        # 수정 로직 진행
        form = UserCustomChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('boards:index')
    else:
        form = UserCustomChangeForm(instance=request.user)
    context = {'form': form,}
    return render(request, 'accounts/auth_form.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST) # 인자 순서 유의
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # 현재 유저가 로그아웃 되는 것을 막음
            return redirect('boards:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    return render(request, 'accounts/auth_form.html', context)
    
def profile(request, user_pk):
    """
    1. 내가 쓴 모든 글 출력
    2. 내가 쓴 댓글들 출력
    3. 작성자를 눌렀을때 프로필로 이동
    """
    user = get_object_or_404(User(), pk=user_pk)
    ctx = {
        'profile_user': user,
    }
    return render(request, 'accounts/profile.html', ctx)