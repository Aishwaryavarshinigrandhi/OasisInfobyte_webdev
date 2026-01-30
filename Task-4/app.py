from flask import Flask, request, redirect, session, render_template_string
import json, os

app = Flask(__name__)
app.secret_key = "json_auth_secret"

USERS_FILE = "users.json"

# ---------- LOAD USERS ----------
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# ---------- SAVE USERS ----------
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------- COMMON CSS ----------
STYLE = """
<style>
body{
    height:100vh;
    margin:0;
    font-family:Arial, sans-serif;
    background:linear-gradient(135deg,#141e30,#243b55);
    display:flex;
    justify-content:center;
    align-items:center;
}
.box{
    background:#fff;
    padding:30px;
    width:360px;
    border-radius:16px;
    text-align:center;
    box-shadow:0 25px 50px rgba(0,0,0,.35);
}
h2{color:#243b55}
p{color:#555}
input{
    width:100%;
    padding:12px;
    margin:10px 0;
}
button{
    width:100%;
    padding:12px;
    background:#243b55;
    color:#fff;
    border:none;
    cursor:pointer;
    border-radius:6px;
}
a{color:#243b55;text-decoration:none;font-weight:bold}
.error{color:red;font-size:0.9rem}
</style>
"""

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        users = load_users()
        for user in users:
            if user["email"] == email and user["password"] == password:
                session["user"] = user["name"]
                return redirect("/dashboard")

        error = "Invalid email or password"

    return render_template_string(STYLE + f"""
        <div class="box">
            <h2>Login</h2>
            <form method="post">
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <p class="error">{error}</p>
            <p>Don't have an account? <a href="/register">Register</a></p>
        </div>
    """)

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        users = load_users()

        for user in users:
            if user["email"] == email:
                error = "Email already registered"
                break
        else:
            users.append({
                "name": name,
                "email": email,
                "password": password
            })
            save_users(users)
            return redirect("/")   # BACK TO LOGIN

    return render_template_string(STYLE + f"""
        <div class="box">
            <h2>Register</h2>
            <form method="post">
                <input name="name" placeholder="Name" required>
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Register</button>
            </form>
            <p class="error">{error}</p>
            <p><a href="/">Back to Login</a></p>
        </div>
    """)

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template_string(STYLE + f"""
        <div class="box">
            <h2>Welcome, {session['user']}</h2>
            <p>This is a secured page 🔐</p>
            <a href="/logout"><button>Logout</button></a>
        </div>
    """)

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
