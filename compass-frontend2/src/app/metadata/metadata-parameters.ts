import {isNullOrUndefined} from "util";
export class MetadataParameters {
  search: string;
  language: string;
  ordering: string;
  limit: number;
  page_size: number;
  page: number;

  toUrlQuery(): string {
    var options_list: string[] = [];

    if (!isNullOrUndefined(this.search)){
      options_list.push('search=' + this.search);
    }
    if (!isNullOrUndefined(this.language)){
      options_list.push('language=' + this.language);
    }
    if (!isNullOrUndefined(this.ordering)){
      options_list.push('ordering=' + this.ordering);
    }
    if(!isNullOrUndefined(this.limit)){
      options_list.push('limit=' + this.limit);
    }
    if(!isNullOrUndefined(this.page_size)){
      options_list.push('page_size=' + this.page_size);
    }
    if(!isNullOrUndefined(this.page)){
      options_list.push('page=' + this.page);
    }
    var query_string = options_list.join('&');
    return '?' + query_string;
  }
}
