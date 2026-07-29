import json
from django.db import models


class AuthorizedUser(models.Model):
    """
    An authorized (known) person. We store their name, photo, and the
    128-dimensional face embedding computed once at enrollment.
    """
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='authorized_faces/')
    # 128 floats serialized as a JSON string
    encoding = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_encoding(self, encoding_array):
        """Store a NumPy embedding as JSON."""
        self.encoding = json.dumps(encoding_array.tolist())

    def get_encoding(self):
        """Return the stored embedding as a Python list, or None."""
        if not self.encoding:
            return None
        return json.loads(self.encoding)

    def __str__(self):
        return self.name