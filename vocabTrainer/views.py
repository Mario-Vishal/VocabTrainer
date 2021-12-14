from django.shortcuts import render, reverse,redirect,HttpResponse,HttpResponseRedirect, get_object_or_404
from .models import VocabCard, TempDeck, Streak
import datetime
from datetime import date
from .forms import VocabCardForm
from next_prev import next_in_order,prev_in_order
#Q objects allows us to perform complex lookups
from django.db.models import Q
# HELPER FUNCTIONS--------------------------------------------------------------------------
def getDate(num=0):
    '''
    returns the date default=0 : today's date
    num = 1 : for tommorow -1 for last seen date on website so on...
    '''
    date_var = datetime.datetime.today().date()
    if num==0:
        return date_var
    elif num==-1:
        return VocabCard.objects.last().date_added
    else:
        return date_var + datetime.timedelta(days=num)

def calStreak(today_date):
    '''
    calculates streak takes input of today's date
    and checks it with the last visited date to calculate
    '''
    
    streak = Streak.objects.last()

    if not streak:
        st = Streak()
        st.date = datetime.datetime.today().date()
        st.count = 1
        st.longest_streak=1
        st.save()
        return [st.count,st.longest_streak]
    last_date_visited = streak.date
   
    if last_date_visited == today_date:
        return [streak.count,streak.longest_streak]
    expected_tommorow_date = last_date_visited + datetime.timedelta(days=1)

    if expected_tommorow_date == today_date:
        streak.count = streak.count+1
        streak.longest_streak = max(streak.count,streak.longest_streak)
        streak.date = today_date
    else:
        streak.longest_streak = max(streak.count,streak.longest_streak)
        streak.date = today_date
        streak.count=1
    streak.save()

    
    return [streak.count,streak.longest_streak]

def getLastAddedDate():
    list_of_dates = VocabCard.objects.values_list('date_added',flat=True).distinct().order_by('-date_added')
    print(list_of_dates)
    if list_of_dates[0]==getDate(0):
        last_added = list_of_dates[1]
    else:
        last_added = list_of_dates[0]
    return last_added
    
def getId(word):
    
    c = VocabCard.objects.get(vocab_word=word)
    return c.id

def getWord(id):
    c = VocabCard.objects.get(pk=id)
    return c.vocab_word

def getObj(id):
    c = VocabCard.objects.get(pk=id)
    return c

def getTotalCount(set_number):
    if set_number>0 and set_number<10000:
        total_count = VocabCard.objects.filter(set_number=set_number).count()
    elif set_number==0:
        total_count = VocabCard.objects.filter(date_added=date.today()).count()
    elif set_number==10001:
        total_count = VocabCard.objects.filter(bookmarked=True).count()
    elif set_number == 10002:
        total_count = VocabCard.objects.filter(date_added=getLastAddedDate()).count()
    
    return total_count

def getFirstLastSetObj():
    '''
    gets the first and the last obj of a set deck
    '''
    vc = TempDeck.objects.all()
    return [ vc.first(),vc.last()]


def printWordId():
    '''
    prints the word ids from TempDeck model
    '''
    vc = TempDeck.objects.all()
    print(list(map(lambda x:x.word_id,vc)))


def createTempDeck(word_ids):
    for word_id in word_ids:
        T = TempDeck()
        T.word_id = word_id
        T.save()

def deleteTempDeck():
    T = TempDeck.objects.all()
    T.delete()


#URL VIEWS--------------------------------------------------------------------------------------

def home(request):
    print("home")
    vocab_cards = VocabCard.objects.all()
    total_words = vocab_cards.count()
    total_sets = VocabCard.objects.values_list('set_number').distinct().count()
    today_date = getDate()
    streak_res = calStreak(today_date)
    count = streak_res[0]
    longest = streak_res[1]
    context = {
        "total_words":total_words,
        "total_sets":total_sets,
        "streak": count,
        "longest":longest,
        "last_seen":getLastAddedDate()
    }

    return render(request,'vocab_trainer/home.html',context)


def bookmark(request,word_id):

    if request.method == 'POST':

        vocab_word = VocabCard.objects.get(pk=word_id)
        print(vocab_word.bookmarked)
        if vocab_word.bookmarked:
            vocab_word.bookmarked = False
        else:
            vocab_word.bookmarked=True
        vocab_word.save()
        print(vocab_word.bookmarked)
        return redirect(request.path_info)
    else:
        return redirect(request.META['HTTP_REFERER'])


def added_today(request):

    vocab_cards = VocabCard.objects.all().filter(date_added = date.today())
    total_count = vocab_cards.count()
    return render(request,'vocab_trainer/added_today.html',{'cards':vocab_cards,"total_count":total_count})

def view_bookmarked(request):

    vocab_cards = VocabCard.objects.filter(bookmarked=True)
    print(vocab_cards)
    return render(request,'vocab_trainer/viewbookmarked.html',{'cards':vocab_cards,"set_number":10001})

def addword(request):

    if request.method == "GET":
        form = VocabCardForm()

        return render(request,"vocab_trainer/addword.html",{'form':form})

    else:
        vCard = VocabCard()
        vCard.vocab_word = request.POST['vocab_word']
        vCard.vocab_pos = request.POST['vocab_pos']
        vCard.vocab_meaning = request.POST['vocab_meaning']
        vCard.vocab_sentence = request.POST['vocab_sentence']

        if request.POST.get('bookmarked')=='on':
            vCard.bookmarked = True
        
        # print(request.POST['vocab_synonyms'])
        vCard.vocab_synonyms = request.POST['vocab_synonyms']
        vCard.save()
        
        return redirect('worddetail',vCard.id)

def word_detail(request,word_id):

    word = get_object_or_404(VocabCard,pk=word_id)
    

    return render(request,"vocab_trainer/detail_card.html",{'card':word})

def edit_word(request,word_id):
    vCard = VocabCard.objects.get(pk=word_id)
    '''
        creating instance of the form so that a user can update the form
    '''
    form = VocabCardForm(request.POST or None,instance=vCard)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect('worddetail',word_id)
    return render(request,"vocab_trainer/edit_delete_card.html",{'form':form,'card_id':word_id})
        

def update_word(request,word_id):
    if request.method=="POST":
        print(request.POST.get('vocab_word'))
        return redirect('worddetail',word_id)

def delete_word(request,word_id):
    vCard = VocabCard.objects.get(pk=word_id)
    vCard.delete()
    return redirect('home')

def search_page(request):
    if request.method == "GET":

        return render(request,"vocab_trainer/search_page.html",{"cards":None})
    else:
        search_index = request.POST['search_index']
        try:
            search_condition = request.POST['search_sentence']
        except:
            search_condition="off"
        if search_condition=="on":
            results = VocabCard.objects.filter(Q(vocab_word__icontains=search_index) | Q(vocab_meaning__icontains=search_index))
        else:
            results = VocabCard.objects.filter(vocab_word__icontains=search_index)
        size = len(results)
        return render(request,"vocab_trainer/search_page.html",{"cards":results,"len":size,"term":search_index})

def set_page(request):

    sets = VocabCard.objects.values_list('set_number').distinct()
    sets = list(map(lambda x: x[0],sets))
    set_words = []
    if sets:
        first_words = list(map(lambda x:VocabCard.objects.filter(set_number=x).first().vocab_word,sets))
        set_list = []
        for i,j in zip(sets,first_words):
            set_list.append((i,j))
        set_words.extend(set_list)
    else:
        first_words = None

    #getting todays list
    today_words = VocabCard.objects.filter(date_added=date.today())
    if today_words:
        today_exist = True
    else:
        today_exist = False
    
    context = {
        "set_words":set_words,
        "today_exists":today_exist
    }

    return render(request,'vocab_trainer/set_revise.html',context)



def set(request,set_number):
    deleteTempDeck()
    print("DELETED TEMP")
    print()
    if set_number == 0:
        data = VocabCard.objects.filter(date_added=date.today()).order_by('?')
    elif set_number == 10001: #10001 is a custom set_number for bookmarked cards
        data = VocabCard.objects.filter(bookmarked=True).order_by('?')
    elif set_number == 10002: #10002 is a custom set_number for last added words
        last_date = getLastAddedDate()
        data = VocabCard.objects.filter(date_added=last_date).order_by('?')
    else:
        data = VocabCard.objects.filter(set_number=set_number).order_by('?')
    word_ids = list(map(lambda x:x.id,data))
    createTempDeck(word_ids)
    print("CREATED TEMP DECK")
    print()
    return redirect('revise_set',set_number)
    # return word_ids
    

#view for url ---> revise_set
def card_slider_main(request,set_number):
    '''
    returns card_next_id card_prev_id to make cards navigatable 
    it's the main function which only runs one navigation is done by
    card_slider_next and card_slider_prev
    '''
    fl = getFirstLastSetObj()
    first_word = fl[0] #first word_id
    last_word = fl[1] #last word_id
    first_id = first_word.word_id

    #prev_id is -1 because every set has to have a first word so there will be no previous word for the first word
    prev_id = -1

    #next_id
    next_word = next_in_order(first_word)
    if next_word:
        next_id = next_word.word_id
    else:
        next_id=-1
    # if not checkNext(next_id,set_number):
    #     next_id=-1


    #current_id
    current_id = first_word.word_id

    #constructing card-id
    #card_id = prev_id---current_id----last_id----current_count

    #last_id
    last_id = last_word.word_id

    #current_count
    current_count = 1

    #card_id
    # card_id = f"{prev_id}_{current_id}_{last_id}_{current_count}"

    #two more card_id's required to navigate through the flash cards
    # 1. card_next_id -> this is used to navigate to the next card which calls the view card_slider_next
    # 2. card_prev_id -> this is used to navigate to the previous card which calls the view card_slider_prev

    #constructing card_next_id
    #card_next_id = current_id---next_id---fast_id---last_id---set_number---current_count
    card_next_id = f"{current_id}_{next_id}_{set_number}_{current_count}"

    #constructing card_prev_id
    #card_prev_id = current_id---next_id---last_id---current_count
    card_prev_id = f"{prev_id}_{current_id}_{set_number}_{current_count}"

    #getting the card details to display the card
    card = get_object_or_404(VocabCard,pk=current_id)


    context = {
        "prev" : -1,
        "current" : current_id,
        "next_" : next_id,
        "card":card,
        "card_next_id":card_next_id,
        "card_prev_id":card_prev_id,
        "total_count": getTotalCount(set_number),
        "current_count":current_count,
        "set_number":set_number
        
    }

    # print("main",context)
    # printWordId()
   

    return render(request,'vocab_trainer/card_slider.html',context)

def card_slider_next(request,card_id):
    '''
    returns the next card_id for the current card_id
    given by the card_slider_main to navigate to the
    next card
    
    '''
    
    list_ids = list(map(int,card_id.split('_')))
    prev_id = list_ids[0]
    current_id = list_ids[1]
    
    set_number = list_ids[2]
    fl = getFirstLastSetObj()
    last_id = fl[1].word_id
    current_count = list_ids[3]+1
    print(current_count)

    if current_id==last_id:
        next_id=-1
    else:
        obj = TempDeck.objects.get(word_id=current_id)
        next_word = next_in_order(obj)
        next_id = next_word.word_id
        # if not checkNext(next_id,set_number):
        #     next_id = -1


    card_next_id = f"{current_id}_{next_id}_{set_number}_{current_count}"
    card_prev_id = f"{prev_id}_{current_id}_{set_number}_{current_count}"

    card = getObj(current_id)

    
    context = {
        "prev" : prev_id,
        "current" : current_id,
        "next_" : next_id,
        "card":card,
        "card_next_id":card_next_id,
        "card_prev_id":card_prev_id,
        "total_count": getTotalCount(set_number),
        "current_count":current_count,
        "set_number":set_number
        
    }

    # print("next",context)
    # printWordId()
    return render(request,'vocab_trainer/card_slider.html',context)
    
    

def card_slider_prev(request,card_id):
    '''
    returns the previous card_id for the current card_id
    given by the card_slider_main to navigate back to the
    previous card
    
    '''
    list_ids = list(map(int,card_id.split('_')))
    current_id = list_ids[0]
    next_id = list_ids[1]

    set_number = list_ids[2]
    current_count = list_ids[3]-1

    fl = getFirstLastSetObj()
    first_id = fl[0].word_id

    current_word = TempDeck.objects.get(word_id=current_id)
    prev_word = prev_in_order(current_word)
    if first_id==current_id:
        prev_id = -1
    else:
        prev_id = prev_word.word_id
    
    card_prev_id = f"{prev_id}_{current_id}_{set_number}_{current_count}"
    card_next_id = f"{current_id}_{next_id}_{set_number}_{current_count}"

    card = getObj(current_id)
    
    context = {
        "prev" : prev_id,
        "current" : current_id,
        "next_" : next_id,
        "card":card,
        "card_next_id":card_next_id,
        "card_prev_id":card_prev_id,
        "total_count": getTotalCount(set_number),
        "current_count":current_count,
        "set_number":set_number
        
    }
    # print("prev",context)
    # printWordId()
    
    return render(request,'vocab_trainer/card_slider.html',context)











