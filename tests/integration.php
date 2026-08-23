<?php

declare(strict_types=1);

require __DIR__ . '/../src/Domain/Appointment.php';
require __DIR__ . '/../src/Domain/AppointmentRepository.php';
require __DIR__ . '/../src/Domain/AvailabilityRepository.php';
require __DIR__ . '/../src/Application/RequestAppointment.php';
require __DIR__ . '/../src/Application/ConfirmAppointment.php';
require __DIR__ . '/../src/Application/CancelAppointment.php';
require __DIR__ . '/../src/Persistence/PdoAppointmentRepository.php';
require __DIR__ . '/../src/Persistence/PdoAvailabilityRepository.php';

use App\Application\CancelAppointment;
use App\Application\ConfirmAppointment;
use App\Application\RequestAppointment;
use App\Domain\Appointment;
use App\Persistence\PdoAppointmentRepository;
use App\Persistence\PdoAvailabilityRepository;

/**
 * Crea una base SQLite en memoria aplicando el esquema real del proyecto.
 * Esto garantiza que las pruebas usen las mismas restricciones e indices
 * definidos en database/schema.sql.
 */
function crearBaseDePrueba(): PDO
{
    $pdo = new PDO('sqlite::memory:');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->exec(file_get_contents(__DIR__ . '/../database/schema.sql'));

    return $pdo;
}

/**
 * Registra la jornada laboral ficticia de un medico para el dia indicado.
 */
function registrarJornada(
    PDO $pdo,
    int $doctorId,
    DateTimeImmutable $fecha
): void {
    $statement = $pdo->prepare(
        'INSERT INTO doctor_availability
            (doctor_id, weekday, start_time, end_time)
         VALUES (:doctor_id, :weekday, :start_time, :end_time)'
    );

    $statement->execute([
        'doctor_id' => $doctorId,
        'weekday' => (int) $fecha->format('w'),
        'start_time' => '08:00:00',
        'end_time' => '17:00:00',
    ]);
}

$tests = [];

$tests['integracion PDO: persiste y recupera la cita'] = function (): void {
    $pdo = crearBaseDePrueba();
    $fecha = new DateTimeImmutable('next monday 10:00');
    registrarJornada($pdo, 2001, $fecha);

    $request = new RequestAppointment(
        new PdoAppointmentRepository($pdo),
        new PdoAvailabilityRepository($pdo)
    );

    $id = $request->execute(1001, 2001, $fecha, 30);

    $guardada = (new PdoAppointmentRepository($pdo))->findById($id);

    if ($guardada === null) {
        throw new RuntimeException('La cita no se recupero desde SQLite.');
    }

    if ($guardada->status() !== Appointment::STATUS_PENDING) {
        throw new RuntimeException('El estado persistido no es pending.');
    }
};

$tests['integracion PDO: rechaza colision de horario'] = function (): void {
    $pdo = crearBaseDePrueba();
    $fecha = new DateTimeImmutable('next monday 10:00');
    registrarJornada($pdo, 2001, $fecha);

    $request = new RequestAppointment(
        new PdoAppointmentRepository($pdo),
        new PdoAvailabilityRepository($pdo)
    );

    $request->execute(1001, 2001, $fecha, 30);

    try {
        $request->execute(1002, 2001, $fecha->modify('+15 minutes'), 30);
    } catch (DomainException $exception) {
        return;
    }

    throw new RuntimeException('Se esperaba rechazo por colision de horario.');
};

$tests['integracion PDO: cancelar libera el horario'] = function (): void {
    $pdo = crearBaseDePrueba();
    $fecha = new DateTimeImmutable('next monday 10:00');
    registrarJornada($pdo, 2001, $fecha);

    $appointments = new PdoAppointmentRepository($pdo);

    $request = new RequestAppointment(
        $appointments,
        new PdoAvailabilityRepository($pdo)
    );

    $id = $request->execute(1001, 2001, $fecha, 30);

    (new CancelAppointment($appointments))->execute($id);

    $nuevoId = $request->execute(1002, 2001, $fecha, 30);

    if ($nuevoId === $id) {
        throw new RuntimeException('No se registro una cita distinta.');
    }
};

$tests['integracion PDO: fuera de jornada no disponible'] = function (): void {
    $pdo = crearBaseDePrueba();
    $fecha = new DateTimeImmutable('next monday 10:00');
    registrarJornada($pdo, 2001, $fecha);

    $request = new RequestAppointment(
        new PdoAppointmentRepository($pdo),
        new PdoAvailabilityRepository($pdo)
    );

    try {
        $request->execute(1001, 2001, $fecha->setTime(20, 0), 30);
    } catch (DomainException $exception) {
        return;
    }

    throw new RuntimeException('Se esperaba rechazo por horario fuera de jornada.');
};

$tests['regla de dominio: no confirmar dos veces'] = function (): void {
    $pdo = crearBaseDePrueba();
    $fecha = new DateTimeImmutable('next monday 10:00');
    registrarJornada($pdo, 2001, $fecha);

    $appointments = new PdoAppointmentRepository($pdo);

    $id = (new RequestAppointment(
        $appointments,
        new PdoAvailabilityRepository($pdo)
    ))->execute(1001, 2001, $fecha, 30);

    $confirm = new ConfirmAppointment($appointments);
    $confirm->execute($id);

    try {
        $confirm->execute($id);
    } catch (DomainException $exception) {
        return;
    }

    throw new RuntimeException('Se esperaba rechazo de confirmacion duplicada.');
};

$tests['regla de dominio: duracion invalida'] = function (): void {
    try {
        Appointment::schedule(1001, 2001, new DateTimeImmutable('+2 days'), 0);
    } catch (DomainException $exception) {
        return;
    }

    throw new RuntimeException('Se esperaba rechazo por duracion invalida.');
};

$passed = 0;
$failed = 0;

foreach ($tests as $name => $test) {
    try {
        $test();

        echo '[OK] ' . $name . PHP_EOL;
        $passed++;
    } catch (Throwable $exception) {
        echo '[FAIL] ' . $name . PHP_EOL;
        echo '       ' . $exception->getMessage() . PHP_EOL;
        $failed++;
    }
}

echo PHP_EOL;
echo 'Resultado: ' . $passed . ' aprobadas, ' . $failed . ' fallidas.' . PHP_EOL;

if ($failed > 0) {
    exit(1);
}

echo 'Todas las pruebas de integracion fueron aprobadas.' . PHP_EOL;
