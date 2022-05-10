import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Article, Cocktail } from '../article-provider/article';
import {ArticleService} from '../article-provider/article.service'

@Component({
  selector: 'app-main-site',
  templateUrl: './main-site.component.html',
  styleUrls: ['./main-site.component.css']
})
export class MainSiteComponent implements OnInit {

  articles: Article[] = [];
  constructor(private articleProvider : ArticleService, private http:HttpClient) { }

  ngOnInit(): void {
    this.getCocktails();
  }

  getCocktails(){
    this.http.get<Cocktail>('http://localhost:5001/cocktails/alfie-cocktail').subscribe(
      data => {
        console.log(data.name);
        console.log(data.slug);
        console.log(data.instructions);
      }
    );
  }

  getArticles(){
    this.articleProvider.getArticles().subscribe(articles => this.articles = articles);
  }
}
