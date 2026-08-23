<?php

echo '== Pruebas unitarias (dobles en memoria) ==' . PHP_EOL;
passthru('php ' . escapeshellarg(__DIR__ . '/run.php'), $unit);

echo PHP_EOL;
echo '== Pruebas de integracion (SQLite via PDO) ==' . PHP_EOL;
passthru('php ' . escapeshellarg(__DIR__ . '/integration.php'), $integration);

echo PHP_EOL;

if ($unit !== 0 || $integration !== 0) {
    echo 'Resultado global: FALLIDO' . PHP_EOL;
    exit(1);
}

echo 'Resultado global: TODAS LAS PRUEBAS APROBADAS' . PHP_EOL;
