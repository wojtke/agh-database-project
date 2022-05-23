import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Article, ArticlesData } from './models';

@Injectable({
  providedIn: 'root'
})

export class ArticleService {
  private articlesUrl = 'http://localhost:5001/articles';

  private  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    })
  };

  constructor(
    private http: HttpClient
  ) { }

  getArticles() : Observable<ArticlesData> {
    return this.http.get<ArticlesData>(this.articlesUrl);
  }

  getRecommendedArticles(id : Number) : Observable<Article[]>{
    return this.http.get<Article[]>(this.articlesUrl + '/recommended');
  }

  getArticlesForUser(id : Number) : Observable<Article[]>{
    return this.http.get<Article[]>(this.articlesUrl + '/user/' + id.toString());
  }

  getArticlesByCategory(category : String) : Observable<Article[]>{
    return this.http.get<Article[]>(this.articlesUrl+'/category/'+category);
  }

  getArticlesByTag(tag : String) : Observable<Article[]>{
    return this.http.get<Article[]>(this.articlesUrl + '/tag/' + tag);
  }

  getArticleById(id : Number) : Observable<Article>{
    return this.http.get<Article>(this.articlesUrl + "/" + id.toString());
  }

  publishAritcle(article : Article){
    this.http.post<Article>(this.articlesUrl, article, this.httpOptions);
  }

  deleteArticle(id : Number){
    this.http.delete(this.articlesUrl + "/" + id.toString());
  }
}


