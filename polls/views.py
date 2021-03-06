from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Question, Choice

'''
Notes :

IDIOMS AND CORRESPONDING SHORTCUTS
#1
Load a template > Fill a context > Render the template (with the context) > Return `HttpResponse`
Shortcut : render()
Syntax : render( request, template, context )
Example : render( request, 'polls/index.html', { 'latest_question_list' : latest_question_list } )

#2
Get an object from model > Raise Http404 if object doesn't exist
Shortcut : get_object_or_404()
Syntax : get_object_or_404( Model, Query )
Example :  get_object_or_404( Question, pk='23' )
'''

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	return render(request, 'polls/index.html', {
		'latest_question_list' : latest_question_list
	})

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {
		'question' : question
	})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {
		'question' : question
	})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
	    # Redisplay the question voting form.
	    return render(request, 'polls/detail.html', {
	        'question': question,
	        'error_message': "You didn't select a choice.",
	    })
	else:
	    selected_choice.votes += 1
	    selected_choice.save()
	    # Always return an HttpResponseRedirect after successfully dealing
	    # with POST data. This prevents data from being posted twice if a
	    # user hits the Back button.
	    # reverse() is used to resolves the url of the view to which we want to pass control;
	    # It helps avoid having to hardcode the URL to th results page
	    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

