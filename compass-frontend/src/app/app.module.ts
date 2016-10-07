import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { Ng2BootstrapModule, PaginationModule  } from 'ng2-bootstrap/ng2-bootstrap';
import { LinkyModule } from 'angular2-linky';

import { AppComponent } from './app.component';
import { MetadataComponent } from './metadata/metadata.component';
import {MetadataService} from "./metadata/metadata.service";
import {routing} from "./app.routing";
import { MetadataDetailComponent } from './metadata/metadata-detail.component';
import {SearchService} from "./metadata/search/search.service";
import {SearchComponent} from "./metadata/search/search.component";
import { SpinnerComponent } from './spinner/spinner.component';


@NgModule({
  declarations: [
    AppComponent,
    MetadataComponent,
    MetadataDetailComponent,
    SearchComponent,
    SpinnerComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    routing,
    HttpModule,
    Ng2BootstrapModule,
    PaginationModule,
    LinkyModule,
  ],
  providers: [
    MetadataService, SearchService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
