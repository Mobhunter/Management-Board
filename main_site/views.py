from datetime import datetime

from django.shortcuts import render, redirect
from .models import Board, Task, Card
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
@login_required(login_url='/login/')
def homepage(request):
	return render(request, "homepage.html", {
		"boards": Board.objects.filter(owner=request.user),
		'user_id': request.user.id,
		})

@login_required(login_url='/login')
def board(request, board_id):
	board = Board.objects.get(id=board_id)
	tasks = Task.objects.filter(board=board)
	paginator = Paginator(tasks, 4)
	page = request.GET.get('page')
	try:
		tasks_s = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		tasks_s = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		tasks_s = paginator.page(paginator.num_pages)
	board_cards = ((task, sorted(Card.objects.filter(task=task), key=lambda x: x.deadline)) for task in tasks_s)
	return render(request, 'board.html', {
			'board': board,
			'board_cards': board_cards,
			'boards': Board.objects.filter(owner=request.user),
			'paginator': paginator,
			'range': list(paginator.page_range),
			'page': tasks_s,
			'user_id': request.user.id,
		})


def log_in(request):
	if request.method == 'POST':
		username = request.POST.get("username", None)
		password = request.POST.get("password", None)
		if all((password, username)):
			check = authenticate(request, username=username, password=password)
			if check:
				login(request, check)
				return redirect("/")
			else:
				return redirect("/error")
		return redirect("/error")
	return render(request, "login.html", {})


def register(request):
	if request.method == "GET":
		return render(request, "register.html", {})
	elif request.method == "POST":
		username = request.POST.get("username", None)
		password = request.POST.get("password", None)
		confirmation = request.POST.get("confirm", None)
		if all((username, password, confirmation, password==confirmation)):
			check = authenticate(request, username=username, password=password)
			if not check:
				try:
					user = User.objects.create_user(username=username, password=password)
					user.save()
					return redirect("/login/")
				except:
					return redirect("/error")
			return redirect("/error")
		return redirect("/error")

@login_required(login_url='/login')
def remove_card(request, id):
	if request.method == "GET":
		card = Card.objects.get(id=id)
		board_id = card.task.board.id
		user = card.task.board.owner
		if user != request.user:
			redirect("/error")
		card.delete()
		return redirect('/board/%d' % board_id)
	return redirect("/error")


@login_required(login_url='/login')
def remove_board(request, id):
	if request.method == "GET":
		board = Board.objects.get(id=id)
		if board.owner != request.user:
			return redirect("/error")
		board.delete()
		return redirect('/')
	return redirect("/error")


@login_required(login_url='/login')
def remove_task(request, id):
	if request.method == "GET":
		task = Task.objects.get(id=id)
		user = task.board.owner
		board_id = task.board.id
		if user != request.user:
			return redirect("/error")
		task.delete()
		return redirect('/board/%d' % board_id)
	return redirect("/error")


@login_required(login_url='/login')
def create_card(request, task_id):
	if request.method == "POST":
		task = Task.objects.get(id=task_id)
		user = task.board.owner
		name = request.POST.get("name", None)
		description = request.POST.get("description", None)
		date = request.POST.get("date", None)
		time = request.POST.get("time", None)
		deadline = datetime.strptime(date + " " + time, "%b %d, %Y %I:%M %p")
		if not all((name, description, deadline)):
			return redirect("/error")
		elif user == request.user:
			card1 = Card(name=name, description=description, deadline=deadline, task=task)
			card1.save()
			return redirect("/board/%d" % task.board.id)
		return redirect("/error")
	elif request.method == "GET":
		current_url = request.get_full_path()
		return render(request, "create_card.html", {})



@login_required(login_url='/login')
def create_task(request, board_id):
	if request.method == "POST":
		board = Board.objects.get(id=board_id)  
		user = board.owner
		name = request.POST.get("name", None)
		if not name:
			return redirect("/error")
		elif user == request.user:
			task1 = Task(name=name, board=board)
			task1.save()
			return redirect("/board/%d" % board.id)
		return redirect("/error")
	elif request.method == "GET":
		return render(request, "create_task.html", {})


@login_required(login_url='/login')
def create_board(request):
	if request.method == "POST":
		user = User.objects.get(id=request.user.id)
		name = request.POST.get("name", None)
		if not name:
			return redirect("/error")
		elif user == request.user:
			board1 = Board(name=name, owner=user)
			board1.save()
			return redirect("/board/%d" % board1.id)
		return redirect("/error")
	elif request.method == "GET":
		return render(request, "create_board.html", {})


def error(request):
	return render(request, "error.html", {})

def logout(request):
	if request.user.is_authenticated():
		logout(request)
		return redirect("/login")