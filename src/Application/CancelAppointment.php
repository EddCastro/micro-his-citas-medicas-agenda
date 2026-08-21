<?php

declare(strict_types=1);

namespace App\Application;

use App\Domain\AppointmentRepository;
use DomainException;

final class CancelAppointment
{
    public function __construct(
        private readonly AppointmentRepository $appointments
    ) {
    }

    public function execute(int $appointmentId): void
    {
        $appointment = $this->appointments->findById($appointmentId);

        if ($appointment === null) {
            throw new DomainException('La cita solicitada no existe.');
        }

        $appointment->cancel();
        $this->appointments->update($appointmentId, $appointment);
    }
}
