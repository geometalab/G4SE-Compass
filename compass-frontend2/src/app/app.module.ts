import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { MetadataComponent } from './metadata/metadata.component';
import {MetadataService} from "./metadata/metadata.service";
import {routing} from "./app.routing";
import { LinkifyPipe } from './metadata/linkify.pipe';

@NgModule({
  declarations: [
    AppComponent,
    MetadataComponent,
    LinkifyPipe
  ],
  imports: [
    BrowserModule,
    FormsModule,
    routing,
    HttpModule
  ],
  providers: [MetadataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
