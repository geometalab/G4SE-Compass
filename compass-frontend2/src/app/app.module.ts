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


@NgModule({
  declarations: [
    AppComponent,
    MetadataComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    routing,
    HttpModule,
    Ng2BootstrapModule,
    PaginationModule,
    LinkyModule
  ],
  providers: [MetadataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
