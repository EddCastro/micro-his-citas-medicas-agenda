<?php

declare(strict_types=1);

namespace App\Domain;

interface AppointmentRepository
{
    public function save(Appointment $appointment): int;

    public function findById(int $id): ?Appointment;

    public function update(int $id, Appointment $appointment): void;
}
