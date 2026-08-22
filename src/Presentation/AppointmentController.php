<?php

declare(strict_types=1);

namespace App\Presentation;

use App\Application\RequestAppointment;
use DateTimeImmutable;

final class AppointmentController
{
    public function __construct(
        private readonly RequestAppointment $requestAppointment
    ) {
    }

    public function create(array $data): int
    {
        return $this->requestAppointment->execute(
            (int) $data['patientId'],
            (int) $data['doctorId'],
            new DateTimeImmutable($data['scheduledAt']),
            (int) $data['durationMinutes']
        );
    }
}
