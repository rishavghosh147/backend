from app import app
from system._system_apis import _system
from admin._admin_apis import _admin
from participants._participants_apis import _participants

app.register_blueprint(_system)
app.register_blueprint(_participants)
app.register_blueprint(_admin)
