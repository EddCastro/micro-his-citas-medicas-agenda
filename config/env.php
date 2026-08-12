<?php

declare(strict_types=1);

function loadEnv(string $filePath): void
{
    if (!is_file($filePath)) {
        throw new RuntimeException("No se encontro el archivo de configuracion.");
    }

    $lines = file($filePath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

    foreach ($lines as $line) {
        $line = trim($line);

        if ($line === '' || str_starts_with($line, '#')) {
            continue;
        }

        [$name, $value] = array_pad(explode('=', $line, 2), 2, '');

        $name = trim($name);
        $value = trim($value);

        if ($name === '') {
            continue;
        }

        $_ENV[$name] = $value;
        putenv($name . '=' . $value);
    }
}
