import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { IngredientClusterComponent } from './ingredient-cluster/ingredient-cluster.component';
import { ExcludeselfPipe } from './excludeself.pipe';

@NgModule({
  declarations: [
    AppComponent,
    IngredientClusterComponent,
    ExcludeselfPipe
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
