from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Messages, Group, UserGroupRelation, GroupMessages
import json
from django.http import JsonResponse
from django.db.models import Q


def getFriendsList(id):
    """
    Get the list of friends of the  user
    :param: user id
    :return: list of friends
    """
    try:
        user = UserProfile.objects.get(id=id)
        ids = user.friends_set.all()
        friends = []
        for id in ids:
            num = str(id)
            fr = UserProfile.objects.get(id=int(num))
            friends.append(fr)
        return friends
    except:
        return []

def getGroupsList(id):
    """
    Get the list of friends of the  user
    :param: user id
    :return: list of friends
    """
    try:
        user_groups_details = UserGroupRelation.objects.filter(user_id=id)
        return user_groups_details
    except:
        return []


def getUserId(username):
    """
    Get the user id by the username
    :param username:
    :return: int
    """
    use = UserProfile.objects.get(username=username)
    id = use.id
    return id


def index(request):
    """
    Return the home page
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        print("Not Logged In!")
        return render(request, "chat/index.html", {})
    else:
        username = request.user.username
        id = getUserId(username)
        friends = getFriendsList(id)
        groups = getGroupsList(id)
        return render(request, "chat/Base.html", {'friends': friends, 'groups':groups})


def search(request):
    """
    Search users page
    :param request:
    :return:
    """
    users = list(UserProfile.objects.all())
    id = getUserId(request.user.username)
    friends = getFriendsList(id)
    groups = getGroupsList(id)
    for user in users:
        if user.username == request.user.username:
            users.remove(user)
            break

    if request.method == "POST":
        print("SEARCHING!!")
        query = request.POST.get("search")
        user_ls = []
        for user in users:
            if query in user.name or query in user.username:
                user_ls.append(user)
        return render(request, "chat/search.html", {'users': user_ls, 'friends': friends, "groups":groups})

    try:
        users = users[:10]
    except:
        users = users[:]

    return render(request, "chat/search.html", {'users': users, 'friends': friends, "groups":groups})


def addFriend(request, name):
    """
    Add a user to the friend's list
    :param request:
    :param name:
    :return:
    """

    username = request.user.username
    id = getUserId(username)
    friend = UserProfile.objects.get(username=name)
    curr_user = UserProfile.objects.get(id=id)
    print(curr_user.name)
    ls = curr_user.friends_set.all()
    flag = 0
    for username in ls:
        if username.friend == friend.id:
            flag = 1
            break
    if flag == 0:
        print("Friend Added!!")
        curr_user.friends_set.create(friend=friend.id)
        friend.friends_set.create(friend=id)
    return redirect("/search")


def chat(request, username):
    """
    Get the chat between two users.
    :param request:
    :param username:
    :return:
    """
    friend = UserProfile.objects.get(username=username)
    id = getUserId(request.user.username)
    curr_user = UserProfile.objects.get(id=id)
    messages = Messages.objects.filter(sender_name=id, receiver_name=friend.id) | Messages.objects.filter(sender_name=friend.id, receiver_name=id)

    if request.method == "GET":
        friends = getFriendsList(id)
        groups = getGroupsList(id)
        return render(request, "chat/messages.html",
                      {'messages': messages,
                       'friends': friends,
                       'curr_user': curr_user, 'friend': friend,
                       'groups':groups})


@csrf_exempt
def update_details(request):
    try:
        body_details = json.loads(request.body.decode("utf-8"))
        user_info = body_details.get("meta")

        Messages.objects.create(sender_name_id=user_info.get("sender_id"),
                                receiver_name_id=user_info.get("receiver_id"),
                                description=body_details.get("message"))

        return JsonResponse({'status':True})
    except Exception as d:
        print(d)
        return JsonResponse({'status': False})



def addgroup(request):

    user_id = request.user.id
    id = getUserId(request.user.username)
    friends = getFriendsList(id)
    groups = getGroupsList(id)
    if request.method == "POST":
        print("ADD group!!")
        group_name = request.POST.get("group-name")

        Group.objects.create(group_name=group_name, created_user_id=user_id)

    group_details = Group.objects.filter(created_user_id=user_id)
    return render(request, "chat/addgroup.html",{"group_details":group_details, 'friends': friends, "groups":groups})


def usergrouprelation(request, groupid):

    id = getUserId(request.user.username)
    friends = getFriendsList(id)
    groups = getGroupsList(id)

    if request.method == "POST":
        user_list = request.POST.getlist('user-list')
        for user in user_list:
            UserGroupRelation.objects.create(group_id=groupid, user_id=user)

    user_ids = UserGroupRelation.objects.filter(group_id=groupid).values("user")
    user_details = UserProfile.objects.filter(~Q(id__in=user_ids))
    added_users = UserProfile.objects.filter(id__in=user_ids)

    return render(request, "chat/groupuserrelation.html",
                  {'friends': friends, "groups":groups,
                   "added_users":added_users, "user_details":user_details})


def groupchat(request, groupid):
    """
    Get the chat between two users.
    :param request:
    :param username:
    :return:
    """
    messages = GroupMessages.objects.filter(group_id=groupid)
    id = getUserId(request.user.username)
    curr_user = UserProfile.objects.get(id=id)
    group = Group.objects.get(id=groupid)

    if request.method == "GET":
        friends = getFriendsList(id)
        groups = getGroupsList(id)
        return render(request, "chat/group_messages.html",
                      {'messages': messages,
                       'group': group,
                       'curr_user': curr_user, 'friends': friends,
                       'groups':groups})



@csrf_exempt
def update_group_details(request):
    try:
        body_details = json.loads(request.body.decode("utf-8"))
        user_info = body_details.get("meta")
        group_id = user_info.get("group_id")
        user_ids = UserGroupRelation.objects.filter(group_id=group_id).\
            exclude(user_id=user_info.get("sender_id")).values_list("user_id", flat=True)
        GroupMessages.objects.create(group_id=group_id, message_parent_id=user_info.get("sender_id"),
                                    message=body_details.get("message"))

        return JsonResponse({'status':True, "users":list(user_ids) if user_ids else [], "message": body_details.get("message")})
    except Exception as d:
        print(d)
        return JsonResponse({'status': False})