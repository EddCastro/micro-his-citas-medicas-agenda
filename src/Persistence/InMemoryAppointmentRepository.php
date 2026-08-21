<?php

declare(strict_types=1);

namespace App\Persistence;

use App\Domain\Appointment;
use App\Domain\AppointmentRepository;
use DateTimeImmutable;

final class InMemoryAppointmentRepository implements AppointmentRepository
{
    private array $appointments = [];

    private int $nextId = 1;

    public function save(Appointment $appointment): int
    {
        $id = $this->nextId++;

        $this->appointments[$id] = $this->toRow($appointment);

        return $id;
    }

    public function findById(int $id): ?Appointment
    {
        if (!isset($this->appointments[$id])) {
            return null;
        }

        $row = $this->appointments[$id];

        return Appointment::restore(
            $row['patient_id'],
            $row['doctor_id'],
            new DateTimeImmutable($row['scheduled_at']),
            $row['duration_minutes'],
            $row['status']
        );
    }

    public function update(int $id, Appointment $appointment): void
    {
        $this->appointments[$id] = $this->toRow($appointment);
    }

    private function toRow(Appointment $appointment): array
    {
        return [
            'patient_id' => $appointment->patientId(),
            'doctor_id' => $appointment->doctorId(),
            'scheduled_at' => $appointment
                ->scheduledAt()
                ->format('Y-m-d H:i:s'),
            'duration_minutes' => $appointment->durationMinutes(),
            'status' => $appointment->status(),
        ];
    }
}
