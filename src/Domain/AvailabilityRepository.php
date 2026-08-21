<?php

declare(strict_types=1);

namespace App\Domain;

use DateTimeImmutable;

interface AvailabilityRepository
{
    public function isAvailable(
        int $doctorId,
        DateTimeImmutable $scheduledAt,
        int $durationMinutes
    ): bool;
}
