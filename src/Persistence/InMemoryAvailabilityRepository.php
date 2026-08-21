<?php

declare(strict_types=1);

namespace App\Persistence;

use App\Domain\AvailabilityRepository;
use DateTimeImmutable;

final class InMemoryAvailabilityRepository implements AvailabilityRepository
{
    public function __construct(
        private bool $available = true
    ) {
    }

    public function isAvailable(
        int $doctorId,
        DateTimeImmutable $scheduledAt,
        int $durationMinutes
    ): bool {
        return $this->available;
    }

    public function setAvailable(bool $available): void
    {
        $this->available = $available;
    }
}
