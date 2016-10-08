from django.shortcuts import render

# Create your views here.
def bet_list(request):
	return render(request, 'casino/bet_list.html', {})