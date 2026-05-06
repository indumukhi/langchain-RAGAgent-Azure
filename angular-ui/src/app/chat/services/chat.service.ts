import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatMessage {
  role: 'user' | 'assistant';
  text: string;
  timestamp: Date;
}

export interface AgentResponse {
  question: string;
  answer: string;
}

@Injectable({ providedIn: 'root' })
export class ChatService {
  private readonly apiUrl = 'http://localhost:8080/api/ask';

  constructor(private http: HttpClient) {}

  ask(question: string): Observable<AgentResponse> {
    return this.http.post<AgentResponse>(this.apiUrl, { question });
  }
}