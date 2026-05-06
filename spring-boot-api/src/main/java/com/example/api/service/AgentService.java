package com.example.api.service;

import com.example.api.dto.AgentResponse;
import com.example.api.dto.QuestionRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class AgentService {

    private static final Logger log = LoggerFactory.getLogger(AgentService.class);

    private final RestClient restClient;

    public AgentService(@Value("${agent.fastapi-url}") String fastapiUrl) {
        this.restClient = RestClient.builder()
                .baseUrl(fastapiUrl)
                .build();
    }

    public AgentResponse ask(String question) {
        log.info("Forwarding question to FastAPI: {}", question);
        return restClient.post()
                .uri("/ask")
                .body(new QuestionRequest(question))
                .retrieve()
                .body(AgentResponse.class);
    }
}