import { Component, OnInit } from '@angular/core';
import { VinosService } from '../vinos.service';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-client',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  providers: [VinosService],
  templateUrl: './client.component.html',
  styleUrl: './client.component.css'
})
export class ClientComponent implements OnInit {

  constructor(private vinosService: VinosService) { }
  ngOnInit(): void {
    // this.recomendaciones()
  }

  vinos: any[] = [];
  sku: string = '';
  errorDetail: string = '';
  agotado: any[] = [];
  selectedVino: any;

  
  data = []
  
  recomendaciones() {
    this.vinos=[];
    this.errorDetail = '';
    const requestData = this.sku.trim();
    // const requestData = 'ESTANCIA-PIEDRA-MAGNUM'
 

    this.vinosService.getVino(requestData).subscribe((response) => {
      console.log('agotado', response);
      if (response.length > 0) {
        this.selectedVino = response[0];
        console.log(this.selectedVino)
      }
    }, (error) => {
      console.error('Error en la solicitud POST:', error);
      // this.errorDetail = error.error.detail; // Asigna el mensaje de error al detalle de error
    });




    // const requestData = 'ESTANCIA-PIEDRA-MAGNUM'; // Los datos que deseas enviar en el cuerpo de la solicitud
    this.vinosService.recomendaciones(requestData).subscribe((response) => {
      console.log('Respuesta de la solicitud POST:', response);
      this.vinos = response;
    }, (error) => {
      console.error('Error en la solicitud POST:', error);
      this.errorDetail = error.error.detail; // Asigna el mensaje de error al detalle de error
    });

    
  }
  
  buscarVino(){
    this.recomendaciones()
  }

}


