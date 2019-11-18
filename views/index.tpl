<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <title>Pigs</title>
</head>

<body>
    <h1>Pigs</h1>
    <p>We do pigs.</p>
    % if random_pigs:
        <p>Here are some random pigs:</p>
        % for pig in random_pigs:
            <li><a href="/pig/{{pig}}/edit">Pig ID {{pig}}</a></li>
        % end
    % end
    <p>
        Do you need <a href="/pig/new">a new pig</a>?
    </p>
</body>

</html>