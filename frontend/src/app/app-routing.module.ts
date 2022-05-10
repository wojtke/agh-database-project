import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainSiteComponent } from './main-site/main-site.component';
import { AddArticleFormComponent } from './add-article-form/add-article-form.component';

const routes: Routes = [
  {path: 'main-site', component: MainSiteComponent},
  {path: 'form', component: AddArticleFormComponent},
  {path: '', redirectTo: '/main-site', pathMatch: 'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
