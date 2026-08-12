<?php

declare(strict_types=1);

namespace App\Domain;

use DateTimeImmutable;
use DomainException;

final class Appointment
{
    public const STATUS_PENDING = 'pending';
    public const STATUS_CONFIRMED = 'confirmed';
    public const STATUS_CANCELLED = 'cancelled';

    private string $status;

    public function __construct(
        private readonly int $patientId,
        private readonly int $doctorId,
        private readonly DateTimeImmutable $scheduledAt,
        private readonly int $durationMinutes
    ) {
        if ($patientId <= 0) {
            throw new DomainException('El paciente es obligatorio.');
        }

        if ($doctorId <= 0) {
            throw new DomainException('El medico es obligatorio.');
        }

        if ($durationMinutes <= 0) {
            throw new DomainException('La duracion debe ser mayor que cero.');
        }

        if ($scheduledAt <= new DateTimeImmutable()) {
            throw new DomainException('La cita debe programarse en una fecha futura.');
        }

        $this->status = self::STATUS_PENDING;
    }

    public function confirm(): void
    {
        if ($this->status === self::STATUS_CANCELLED) {
            throw new DomainException('Una cita cancelada no puede confirmarse.');
        }

        $this->status = self::STATUS_CONFIRMED;
    }

    public function cancel(): void
    {
        if ($this->status === self::STATUS_CANCELLED) {
            throw new DomainException('La cita ya se encuentra cancelada.');
        }

        $this->status = self::STATUS_CANCELLED;
    }

    public function patientId(): int
    {
        return $this->patientId;
    }

    public function doctorId(): int
    {
        return $this->doctorId;
    }

    public function scheduledAt(): DateTimeImmutable
    {
        return $this->scheduledAt;
    }

    public function durationMinutes(): int
    {
        return $this->durationMinutes;
    }

    public function status(): string
    {
        return $this->status;
    }
}
