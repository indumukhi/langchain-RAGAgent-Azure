package com.example.api.controller;

import com.example.api.dto.AgentResponse;
import com.example.api.dto.QuestionRequest;
import com.example.api.service.AgentService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:4200")
public class QuestionController {

    private final AgentService agentService;

    public QuestionController(AgentService agentService) {
        this.agentService = agentService;
    }

    @PostMapping("/ask")
    public AgentResponse ask(@Valid @RequestBody QuestionRequest request) {
        return agentService.ask(request.question());
    }

    @GetMapping("/health")
    public String health() {
        return "OK";
    }
}