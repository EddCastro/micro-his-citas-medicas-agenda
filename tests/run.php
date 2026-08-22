<?php

declare(strict_types=1);

require __DIR__ . '/../src/Domain/Appointment.php';
require __DIR__ . '/../src/Domain/AppointmentRepository.php';
require __DIR__ . '/../src/Domain/AvailabilityRepository.php';

require __DIR__ . '/../src/Application/RequestAppointment.php';
require __DIR__ . '/../src/Application/ConfirmAppointment.php';
require __DIR__ . '/../src/Application/CancelAppointment.php';

require __DIR__ . '/../src/Persistence/InMemoryAppointmentRepository.php';
require __DIR__ . '/../src/Persistence/InMemoryAvailabilityRepository.php';

use App\Application\CancelAppointment;
use App\Application\ConfirmAppointment;
use App\Application\RequestAppointment;
use App\Domain\Appointment;
use App\Domain\AppointmentRepository;
use App\Persistence\InMemoryAppointmentRepository;
use App\Persistence\InMemoryAvailabilityRepository;

$tests = [];

$tests['camino feliz: solicitar, confirmar y cancelar'] = function (): void {
    $appointments = new InMemoryAppointmentRepository();
    $availability = new InMemoryAvailabilityRepository(true);

    $request = new RequestAppointment(
        $appointments,
        $availability
    );

    $id = $request->execute(
        1001,
        2001,
        new DateTimeImmutable('+2 days 10:00'),
        30
    );

    $created = $appointments->findById($id);

    if (
        $created === null ||
        $created->status() !== Appointment::STATUS_PENDING
    ) {
        throw new RuntimeException(
            'La cita no fue creada en estado pending.'
        );
    }

    $confirm = new ConfirmAppointment($appointments);
    $confirm->execute($id);

    $confirmed = $appointments->findById($id);

    if (
        $confirmed === null ||
        $confirmed->status() !== Appointment::STATUS_CONFIRMED
    ) {
        throw new RuntimeException(
            'La cita no fue confirmada.'
        );
    }

    $cancel = new CancelAppointment($appointments);
    $cancel->execute($id);

    $cancelled = $appointments->findById($id);

    if (
        $cancelled === null ||
        $cancelled->status() !== Appointment::STATUS_CANCELLED
    ) {
        throw new RuntimeException(
            'La cita no fue cancelada.'
        );
    }
};

$tests['regla: horario no disponible'] = function (): void {
    $appointments = new InMemoryAppointmentRepository();
    $availability = new InMemoryAvailabilityRepository(false);

    $request = new RequestAppointment(
        $appointments,
        $availability
    );

    try {
        $request->execute(
            1001,
            2001,
            new DateTimeImmutable('+2 days 10:00'),
            30
        );
    } catch (DomainException $exception) {
        return;
    }

    throw new RuntimeException(
        'Se esperaba rechazo por horario no disponible.'
    );
};

$tests['regla de dominio: fecha pasada'] = function (): void {
    try {
        Appointment::schedule(
            1001,
            2001,
            new DateTimeImmutable('-1 day'),
            30
        );
    } catch (DomainException $exception) {
        return;
    }

    throw new RuntimeException(
        'Se esperaba rechazo de una cita en fecha pasada.'
    );
};

$tests['error de persistencia mediante doble'] = function (): void {
    $failingRepository = new class implements AppointmentRepository {
        public function save(Appointment $appointment): int
        {
            throw new RuntimeException(
                'Error simulado de persistencia.'
            );
        }

        public function findById(int $id): ?Appointment
        {
            return null;
        }

        public function update(
            int $id,
            Appointment $appointment
        ): void {
        }
    };

    $availability = new InMemoryAvailabilityRepository(true);

    $request = new RequestAppointment(
        $failingRepository,
        $availability
    );

    try {
        $request->execute(
            1001,
            2001,
            new DateTimeImmutable('+2 days 10:00'),
            30
        );
    } catch (RuntimeException $exception) {
        if (
            $exception->getMessage() ===
            'Error simulado de persistencia.'
        ) {
            return;
        }

        throw $exception;
    }

    throw new RuntimeException(
        'Se esperaba un error de persistencia.'
    );
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
echo 'Resultado: ' .
    $passed . ' aprobadas, ' .
    $failed . ' fallidas.' .
    PHP_EOL;

if ($failed > 0) {
    exit(1);
}

echo 'Todas las pruebas fueron aprobadas.' . PHP_EOL;
