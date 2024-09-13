
from ..models import Rating, NormalizedRatingParameters, Saves, addrecipe
import collections
import numpy as np

def setZScoreParameters(user):
    r=[]
    if Rating.objects.filter(user=user).exists():
        for i in Rating.objects.filter(user=user):
            r.append(i.rating)
    else:
        if NormalizedRatingParameters.objects.filter(user=user).exists():
            a=NormalizedRatingParameters.objects.get(user=user)
            a.delete()
    mean_rating = np.mean(r)
    std_dev = np.std(r)
    if NormalizedRatingParameters.objects.filter(user=user).exists():
        a=NormalizedRatingParameters.objects.get(user=user)
        a.std=std_dev
        a.mean=mean_rating
        a.save()
    else:
        NormalizedRatingParameters.objects.create(user=user,std=std_dev,mean=mean_rating)

def normalizedRating(user,rating):
    if Rating.objects.filter(user=user).exists() and not NormalizedRatingParameters.objects.filter(user=user):
        setZScoreParameters(user)
    t=[0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]
    param=NormalizedRatingParameters.objects.get(user=user)
    if param.std==0:
        z_score=0
    else:
        z_score = (float(rating) - param.mean) / param.std
    return round((float(z_score)*np.std(t))+np.mean(t),2)

def getUserScore(user):
    if not Rating.objects.filter(user=user).exists():
        return []
    allUserRatings=Rating.objects.filter(user=user)
    d=collections.defaultdict(int)
    for i in allUserRatings:
        othersRating = Rating.objects.filter(recipe = i.recipe)
        uRating=normalizedRating(user,i.rating)
        for j in othersRating:
            if j.user != user:
                oRating=normalizedRating(j.user,j.rating)
                if abs(oRating - uRating) <= 0.25:
                    d[j.user]+=5
                elif abs(oRating - uRating) <= 0.5:
                    d[j.user]+=3.5
                elif abs(oRating - uRating) <= 1.0:
                    d[j.user]+=2
                elif abs(oRating - uRating) <= 1.5:
                    d[j.user]+=0.5
                elif abs(oRating - uRating) <= 2.0:
                    d[j.user]+=0
                elif abs(oRating - uRating) <= 2.5:
                    d[j.user]-=0.5
                elif abs(oRating - uRating) <= 3.0:
                    d[j.user]-=2.0
                elif abs(oRating - uRating) <= 3.5:
                    d[j.user]-=3.5
                else:
                    d[j.user]-=5.0
    l=[]
    for i in d:
        l.append((i,d[i]))
    return l


def getPosts(user, other):
    unRatedList=[]
    otherUsersRatings=Rating.objects.filter(user=other)
    for i in otherUsersRatings:
        if not Rating.objects.filter(user=user,recipe=i.recipe).exists():
            unRatedList.append(i.recipe)
    return unRatedList

def ratePosts(posts,userScore):
    d=collections.defaultdict(int)
    for i in posts:
        for j in userScore:
            if Rating.objects.filter(user=j[0],recipe=i).exists():
                d[i]+=(j[1]*float(Rating.objects.get(user=j[0],recipe=i).rating))

    res=[]
    for i in d:
        res.append((i,d[i]))
    res.sort(key= lambda x:x[1],reverse=True)
    l=[]
    maxScore=res[0][1]
    for i in res:
        l.append({'recipe':i[0],'score':i[1],'percentage':round((i[1]/maxScore)*100,2),})
    #print(l)
    return l

def recommendedPosts(user):
    userScore=getUserScore(user)
    userScore.sort(key= lambda x:x[1],reverse=True)
    print(userScore)

    if userScore==[]:
        return None
    
    count=0
    posts=set()
    for i in userScore:
        if i[1]<=0:
            break
        for j in getPosts(user,i[0]):
            posts.add(j)
        count+=1
        if count>5 and len(posts)>=10:
            break
    
    print(posts)
    if len(posts)==0:
        return None
    return ratePosts(posts,userScore[:count])

def popular():
    d=collections.defaultdict(int)
    for i in addrecipe.objects.all():
        if Rating.objects.filter(recipe=i).exists():
            d[i]+=len(Rating.objects.filter(recipe=i))
        if Saves.objects.filter(recipe=i).exists():
            d[i]+=2*len(Saves.objects.filter(recipe=i))
    l=[]
    for i in d:
        l.append((i,d[i]))
    l.sort(key= lambda x:x[1], reverse=True)
    r=[]
    count=0
    for i in l:
        r.append(i[0])
        count+=1
        if count==10:
            break
    return r

def topRated():
    d=collections.defaultdict(int)
    m=float(2)
    c=float(np.mean(list(Rating.objects.values_list('rating',flat=True))))
    print("c:",c)
    for i in addrecipe.objects.all():
        if Rating.objects.filter(recipe=i).exists():
            v=float(len(Rating.objects.filter(recipe=i)))
            avg=np.average(list(Rating.objects.filter(recipe=i).values_list('rating',flat=True)))
            avg=float(avg)
            print(i.name,":",v,avg)
            d[i]=(float(v/(v+m))*avg)+((m/(v+m))*c)
    l=[]

    for i in d:
        l.append((i,d[i]))
    l.sort(key= lambda x:x[1], reverse=True)
    r=[]
    count=0
    for i in l:
        r.append(i[0])
        count+=1
        if count==10:
            break
    return r