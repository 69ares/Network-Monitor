Strumento per la sicurezza informatica che utilizza il comando "netstat" per monitorare le connessioni attive in un sistema e l'API di AbuseIPDB 
per verificare la reputazione degli indirizzi IP connessi. 

Utilizza una GUI basata su Tkinter per chiedere all'utente di inserire la propria chiave API e una soglia di punteggio di reputazione. 
Se un indirizzo IP connesso ha un punteggio di reputazione superiore a quella soglia, verrà segnalato all'utente e verrà chiesto se terminare il processo associato. 
Inoltre, registra gli indirizzi IP considerati sicuri e pericolosi in file di testo separati. 

Potrebbe essere utilizzato come soluzione di sicurezza in ambienti aziendali per prevenire attacchi informatici e proteggere i sistemi da connessioni dannose. 



Features:
- INTEGRAZIONE FIREWALL
- RUNNING IN BACKGROUND MODALITA' SILENTE
- CHECK CHIAMATE API RIMANENTI
- GUI DELLA MODALITA LIVE-MONITORING

API:
- AbuseIPDB

Future integrazioni:
- VirusTotal
- Shodan
- MISP
