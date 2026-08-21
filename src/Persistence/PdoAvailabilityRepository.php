<?php

declare(strict_types=1);

namespace App\Persistence;

use App\Domain\Appointment;
use App\Domain\AvailabilityRepository;
use DateTimeImmutable;
use PDO;

final class PdoAvailabilityRepository implements AvailabilityRepository
{
    public function __construct(
        private readonly PDO $pdo
    ) {
    }

    public function isAvailable(
        int $doctorId,
        DateTimeImmutable $scheduledAt,
        int $durationMinutes
    ): bool {
        $scheduledEnd = $scheduledAt->modify(
            '+' . $durationMinutes . ' minutes'
        );

        $availabilityStatement = $this->pdo->prepare(
            'SELECT COUNT(*)
            FROM doctor_availability
            WHERE doctor_id = :doctor_id
              AND weekday = :weekday
              AND start_time <= :start_time
              AND end_time >= :end_time'
        );

        $availabilityStatement->execute([
            'doctor_id' => $doctorId,
            'weekday' => (int) $scheduledAt->format('w'),
            'start_time' => $scheduledAt->format('H:i:s'),
            'end_time' => $scheduledEnd->format('H:i:s'),
        ]);

        if ((int) $availabilityStatement->fetchColumn() === 0) {
            return false;
        }

        $collisionStatement = $this->pdo->prepare(
            "SELECT COUNT(*)
            FROM appointments
            WHERE doctor_id = :doctor_id
              AND status != :cancelled_status
              AND scheduled_at < :requested_end
              AND datetime(
                    scheduled_at,
                    '+' || duration_minutes || ' minutes'
                  ) > :requested_start"
        );

        $collisionStatement->execute([
            'doctor_id' => $doctorId,
            'cancelled_status' => Appointment::STATUS_CANCELLED,
            'requested_start' => $scheduledAt->format('Y-m-d H:i:s'),
            'requested_end' => $scheduledEnd->format('Y-m-d H:i:s'),
        ]);

        return (int) $collisionStatement->fetchColumn() === 0;
    }
}
