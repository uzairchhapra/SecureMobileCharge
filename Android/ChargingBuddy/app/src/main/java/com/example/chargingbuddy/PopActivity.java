package com.example.chargingbuddy;
import android.app.Activity;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.Gravity;
import android.view.WindowManager;
import android.widget.LinearLayout;
import android.widget.TableRow;
import android.widget.TextView;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class PopActivity extends Activity {

    //     <!-- Get stations
    public class GetStations extends AsyncTask<String, Void, String> {


        @Override
        protected String doInBackground(String... strings) {

            String result = "";
            URL url;
            HttpURLConnection conn;
            try {
                url = new URL("http://192.168.43.237:8000/charge/checkslots?stationid="+strings[0]+"&device=android");
                conn = (HttpURLConnection) url.openConnection();
                InputStream in = conn.getInputStream();
                InputStreamReader reader = new InputStreamReader(in);
                int data = reader.read();
                while (data != -1) {
                    char current = (char) data;
                    result += current;
                    data = reader.read();
                }
            } catch (Exception e) {
                result += "Error: ";
                result += e.getMessage();
            }


            Log.d("result", "onMapReady: Popup doInBackGround");
            return result;
        }

        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            Log.d("result", "Popup onPostExecute: "+result);

            int[] status = status_stations(result);
            TextView slot1 = findViewById(R.id.slot1);
            TextView slot2 = findViewById(R.id.slot2);
            TextView slot3 = findViewById(R.id.slot3);
            TextView slot4 = findViewById(R.id.slot4);
            TextView slot1_1 = findViewById(R.id.slot1_1);
            TextView slot1_2 = findViewById(R.id.slot1_2);
            TextView slot2_1 = findViewById(R.id.slot2_1);
            TextView slot2_2 = findViewById(R.id.slot2_2);
            TextView slot3_1 = findViewById(R.id.slot3_1);
            TextView slot3_2 = findViewById(R.id.slot3_2);
            TextView slot4_1 = findViewById(R.id.slot4_1);
            TextView slot4_2 = findViewById(R.id.slot4_2);


            if (status[0]==-1){
                slot1_1.setText("Already in use");
                slot1_2.setText("Check after sometime");
                slot1.setBackgroundResource(R.drawable.round_red);
            }
            else{
                slot1_1.setText(""+status[0]+" Slot Id");
                slot1_2.setText("Ready to use");
                slot1.setBackgroundResource(R.drawable.round_green);
            }

            if (status[1]==-1){
                slot2_1.setText("Already in use");
                slot2_2.setText("Check after sometime");
                slot2.setBackgroundResource(R.drawable.round_red);
            }
            else{
                slot2_1.setText(""+status[1]+" Slot Id");
                slot2_2.setText("Ready to use");
                slot2.setBackgroundResource(R.drawable.round_green);
            }

            if (status[2]==-1){
                slot3_1.setText("Already in use");
                slot3_2.setText("Check after sometime");
                slot3.setBackgroundResource(R.drawable.round_red);
            }
            else{
                slot3_1.setText(""+status[2]+" Slot Id");
                slot3_2.setText("Ready to use");
                slot3.setBackgroundResource(R.drawable.round_green);
            }

            if (status[3]==-1){
                slot4_1.setText("Already in use");
                slot4_2.setText("Check after sometime");
                slot4.setBackgroundResource(R.drawable.round_red);
            }
            else{
                slot4_1.setText(""+status[3]+" Slot Id");
                slot4_2.setText("Ready to use");
                slot4.setBackgroundResource(R.drawable.round_green);
            }

        }
    }
//    Get stations>>


    private int[] status_stations(String result){
        int[] status = {-1,-1,-1,-1};
        String s=result.trim();
        String t[]=s.split("\\{")[2].split("\\}")[0].split(",");
        int index,value;
        String x;
        if (t[0].length()>0) {
            for (int j = 0; j < t.length; j++) {
                x = t[j];
                x = x.trim();
                index = Integer.parseInt(x.substring(1, x.indexOf("\"", 1)));
                value = Integer.parseInt(x.substring(x.lastIndexOf(":") + 1).trim());
                status[index] = value;
            }
        }
        return status;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pop);

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        int width = dm.widthPixels;
        int height = dm.heightPixels;
        getWindow().setLayout((int)(width*.8),(int)(height*.6 ));
        getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));

        LinearLayout tl = findViewById(R.id.tl);
        LinearLayout dl = findViewById(R.id.dl);
        LinearLayout tr = findViewById(R.id.tr);
        LinearLayout dr = findViewById(R.id.dr);

        int station_height = tl.getLayoutParams().height;

        findViewById(R.id.tl).setLayoutParams(new TableRow.LayoutParams((int)(width*.4),station_height));
        findViewById(R.id.dl).setLayoutParams(new TableRow.LayoutParams((int)(width*.4),station_height));
        findViewById(R.id.tr).setLayoutParams(new TableRow.LayoutParams((int)(width*.4),station_height));
        findViewById(R.id.dr).setLayoutParams(new TableRow.LayoutParams((int)(width*.4),station_height));

        tl.setPadding(2,2,2,2);
        dl.setPadding(2,2,2,2);
        tr.setPadding(2,2,2,2);
        dr.setPadding(2,2,2,2);

        WindowManager.LayoutParams params=getWindow().getAttributes();
        params.gravity= Gravity.CENTER;
        params.x=0;
        params.y=-20;
        getWindow().setAttributes(params);
        TextView tv_name = findViewById(R.id.textViewName);
        TextView tv_desc = findViewById(R.id.textViewDesc);
        tv_name.setText(getIntent().getExtras().getString("name"));
        tv_desc.setText(getIntent().getExtras().getString("s"));

        GetStations getStations= new GetStations();
        getStations.execute(""+getIntent().getExtras().getString("id"));

    }
}
