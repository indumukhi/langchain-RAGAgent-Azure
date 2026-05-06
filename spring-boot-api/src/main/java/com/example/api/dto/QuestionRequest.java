package com.example.api.dto;

import jakarta.validation.constraints.NotBlank;

public record QuestionRequest(@NotBlank String question) {}