import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class VinosService {

  constructor(private http: HttpClient) { }

  // Método para realizar una solicitud GET a la URL 'get_vino'
  getVino(sku:string) {
    return this.http.get<any>('http://localhost:8000/vino_agotado/'+sku);
  }

  // Método para realizar una solicitud POST a la URL 'vinostodos'
  recomendaciones(data: any) {
    data = {'SKU': data}
    return this.http.post<any>('http://localhost:8000/obtener_vinos_similares_con_m_embeding/', data);
  }

}
