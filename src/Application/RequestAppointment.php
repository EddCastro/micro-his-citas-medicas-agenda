<?php

declare(strict_types=1);

namespace App\Application;

use App\Domain\Appointment;
use App\Domain\AppointmentRepository;
use App\Domain\AvailabilityRepository;
use DateTimeImmutable;
use DomainException;

final class RequestAppointment
{
    public function __construct(
        private readonly AppointmentRepository $appointments,
        private readonly AvailabilityRepository $availability
    ) {
    }

    public function execute(
        int $patientId,
        int $doctorId,
        DateTimeImmutable $scheduledAt,
        int $durationMinutes
    ): int {
        if (!$this->availability->isAvailable(
            $doctorId,
            $scheduledAt,
            $durationMinutes
        )) {
            throw new DomainException('El horario seleccionado no esta disponible.');
        }

        $appointment = new Appointment(
            $patientId,
            $doctorId,
            $scheduledAt,
            $durationMinutes
        );

        return $this->appointments->save($appointment);
    }
}
