import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Article} from '../services/models';
import {ArticleService} from '../services//article.service'
import { AppModule } from '../app.module';

@Component({
  selector: 'app-main-site',
  templateUrl: './main-site.component.html',
  styleUrls: ['./main-site.component.css']
})
export class MainSiteComponent implements OnInit {

  articles: Article[] = [];
  recent_articles  : Article[] = [];
  usedLoggedIn : Boolean = AppModule.current_user.login === "";
  constructor(private articleProvider : ArticleService, private http:HttpClient) { }

  ngOnInit(): void {
    this.getArticles();
    this.getRecent();
  }

  getRecent(){
    this.articleProvider.getArticles().subscribe(data =>{
      this.recent_articles = data.articles.slice(-4, -1);
    } );

  }

  getArticles(){
    this.articleProvider.getArticles().subscribe(data =>{
      this.articles = data.articles.slice(0, 3);
    } );
  }
}
