from django.db import models


class UserProfile(models.Model):

    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"


class Messages(models.Model):

    description = models.TextField()
    sender_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    receiver_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver')
    time = models.TimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.receiver_name} From: {self.sender_name}"

    class Meta:
        ordering = ('timestamp',)


class Friends(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    friend = models.IntegerField()

    def __str__(self):
        return f"{self.friend}"

class Group(models.Model):

    group_name = models.CharField(max_length=300)
    created_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class UserGroupRelation(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class GroupMessages(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    message_parent = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    time = models.TimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)