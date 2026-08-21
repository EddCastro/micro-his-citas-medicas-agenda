<?php

declare(strict_types=1);

namespace App\Persistence;

use App\Domain\Appointment;
use App\Domain\AppointmentRepository;
use DateTimeImmutable;
use PDO;

final class PdoAppointmentRepository implements AppointmentRepository
{
    public function __construct(
        private readonly PDO $pdo
    ) {
    }

    public function save(Appointment $appointment): int
    {
        $statement = $this->pdo->prepare(
            'INSERT INTO appointments (
                patient_id,
                doctor_id,
                scheduled_at,
                duration_minutes,
                status
            ) VALUES (
                :patient_id,
                :doctor_id,
                :scheduled_at,
                :duration_minutes,
                :status
            )'
        );

        $statement->execute([
            'patient_id' => $appointment->patientId(),
            'doctor_id' => $appointment->doctorId(),
            'scheduled_at' => $appointment->scheduledAt()->format('Y-m-d H:i:s'),
            'duration_minutes' => $appointment->durationMinutes(),
            'status' => $appointment->status(),
        ]);

        return (int) $this->pdo->lastInsertId();
    }

    public function findById(int $id): ?Appointment
    {
        $statement = $this->pdo->prepare(
            'SELECT
                patient_id,
                doctor_id,
                scheduled_at,
                duration_minutes,
                status
            FROM appointments
            WHERE id = :id'
        );

        $statement->execute([
            'id' => $id,
        ]);

        $row = $statement->fetch(PDO::FETCH_ASSOC);

        if ($row === false) {
            return null;
        }

        return Appointment::restore(
            (int) $row['patient_id'],
            (int) $row['doctor_id'],
            new DateTimeImmutable((string) $row['scheduled_at']),
            (int) $row['duration_minutes'],
            (string) $row['status']
        );
    }

    public function update(int $id, Appointment $appointment): void
    {
        $statement = $this->pdo->prepare(
            'UPDATE appointments
            SET status = :status
            WHERE id = :id'
        );

        $statement->execute([
            'status' => $appointment->status(),
            'id' => $id,
        ]);
    }
}
