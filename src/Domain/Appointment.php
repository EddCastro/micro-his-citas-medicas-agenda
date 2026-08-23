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

    private function __construct(
        private readonly int $patientId,
        private readonly int $doctorId,
        private readonly DateTimeImmutable $scheduledAt,
        private readonly int $durationMinutes,
        private string $status
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

        if (!in_array($status, [
            self::STATUS_PENDING,
            self::STATUS_CONFIRMED,
            self::STATUS_CANCELLED,
        ], true)) {
            throw new DomainException('El estado de la cita no es valido.');
        }
    }

    public static function schedule(
        int $patientId,
        int $doctorId,
        DateTimeImmutable $scheduledAt,
        int $durationMinutes
    ): self {
        if ($scheduledAt <= new DateTimeImmutable()) {
            throw new DomainException('La cita debe programarse en una fecha futura.');
        }

        return new self(
            $patientId,
            $doctorId,
            $scheduledAt,
            $durationMinutes,
            self::STATUS_PENDING
        );
    }

    public static function restore(
        int $patientId,
        int $doctorId,
        DateTimeImmutable $scheduledAt,
        int $durationMinutes,
        string $status
    ): self {
        return new self(
            $patientId,
            $doctorId,
            $scheduledAt,
            $durationMinutes,
            $status
        );
    }

    public function confirm(): void
    {
        if ($this->status === self::STATUS_CANCELLED) {
            throw new DomainException('Una cita cancelada no puede confirmarse.');
        }

        if ($this->status === self::STATUS_CONFIRMED) {
            throw new DomainException('La cita ya se encuentra confirmada.');
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
