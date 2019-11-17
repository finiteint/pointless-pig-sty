<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <title>Edit {{ name }}</title>
</head>

<body>
    <h1>Edit {{ name }}</h1>
    <form action="/pig/{{key}}/update" method="post">
        <div>
            <label for="name">Pig's Name:</label>
            <input type="text" id="name" name="name" value="{{ name }}">
        </div>
        <div>
            <label for="data">Pig's Data:</label>
            <textarea id="data" name="data">{{ data }}</textarea>
        </div>
        <div>
            <button type="submit">Update Pig</button>
        </div>
    </form>
</body>

</html>