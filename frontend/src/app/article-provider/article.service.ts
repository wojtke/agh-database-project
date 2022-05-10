import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Article } from './article';

@Injectable({
  providedIn: 'root'
})

export class ArticleService {
  private articlesUrl = 'http://localhost:5001/articles';
  constructor(
    private http: HttpClient
  ) { }

  getArticles() : Observable<Article[]> {
    return this.http.get<Article[]>(this.articlesUrl);
  }
}


