export class Article{
  article_id: Number;
  title: String;
  tags: String[];
  category: String;
  content: String;
  image_source: String;
  grades: Number;
  sumGrades: Number;
  views: Number;
  addDate: Date;

  constructor(){
    this.article_id = 0;
    this.title = '';
    this.tags = [];
    this.category = '';
    this.content = '';
    this.image_source = '';
    this.grades = 0;
    this.sumGrades = 0;
    this.views = 0;
    this.addDate = new Date();
  }
}

export interface LinksArticles{
  links: String[];
  articles: Article[];
}

export interface View{
  article_id: Number,
  value: Number
}

export class Rating{
  article_id: Number;
  value: Number;

  constructor(){
    this.article_id = 0;
    this.value = 0;
  }
}

export class User{
  id: Number;
  name: String;
  login: String;
  ratings: Rating[];
  views: View[];

  constructor(
    id = 0,
    name = '',
    login = '',
    ratings = [],
    views = [], ){
      this.id = id;
      this.name = name;
      this.login = login;
      this.ratings = ratings;
      this.views = views;
  }
}

export interface LinksUsers{
    links: String[],
    users: User[]
}

export class Comment{
  id: Number;
  user_id: Number;
  article_id: Number;
  content: String;

  constructor(){
    this.id = 0;
    this.user_id = 0;
    this.article_id = 0;
    this.content = '';
  }
}
