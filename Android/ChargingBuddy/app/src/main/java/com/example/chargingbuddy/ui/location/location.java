package com.example.chargingbuddy.ui.location;

import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.FragmentTransaction;
import androidx.lifecycle.ViewModelProviders;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.AsyncTask;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import com.example.chargingbuddy.PopActivity;
import com.example.chargingbuddy.R;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;


import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;


class locations {
    int id;
    double lat;
    double lng;
    String s;
    String name;

    locations(int id, double lat, double lng, String s, String name) {
        this.id = id;
        this.lat = lat;
        this.lng = lng;
        this.s = s;
        this.name = name;
    }

    @Override
    public String toString() {
        return ("" + this.id + " " + this.lat + " " + this.lng + " " + this.s + " " + this.name);
    }

}

public class location extends Fragment implements OnMapReadyCallback, GoogleMap.OnMarkerClickListener {

    //     <!-- Get markers
    public class GetMarkers extends AsyncTask<String, Void, String> {

        GoogleMap m;

        @Override
        protected String doInBackground(String... strings) {

            String result = "";
            URL url;
            HttpURLConnection conn;
            try {
                url = new URL("http://192.168.43.237:8000/charge/getlocation");
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

            Log.d("result", "onMapReady: Location doInBackGround");

            return result;
        }

        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
//        Log.d("result", "onPostExecute: "+result);

            LatLng marker;
            locations stations[] = string_to_loc_class(result);

            for (int j = 0; j < stations.length; j++) {
                Log.d("result_sta", "doInBackground: " + stations[j]);

                marker = new LatLng(stations[j].lat, stations[j].lng);
                m.addMarker(new MarkerOptions().position(marker)).setTag(stations[j]);

            }
        }
    }
//    Get markers>>


    private locations[] string_to_loc_class(String s) {
        int i = s.indexOf("id");
        locations l[];

        if (i != -1) {
            String arr[] = s.split("\"id\"");
            l = new locations[arr.length - 1];

            for (int j = 1; j < arr.length; j++) {
                int id;
                double lat, lng;
                String data, name;

                String t = arr[j];
                int start = t.indexOf(":") + 2;
                int end = t.indexOf(",");
                id = Integer.parseInt(t.substring(start, end));

                t = t.substring(end + 1);
                start = t.indexOf(":") + 3;
                end = t.indexOf(",") - 1;
                lat = Double.parseDouble(t.substring(start, end));

                t = t.substring(end + 1);
                start = t.indexOf(":") + 3;
                end = t.indexOf(",", 2) - 1;
                lng = Double.parseDouble(t.substring(start, end));

                t = t.substring(end + 1);
                start = t.indexOf(":") + 3;
                end = t.indexOf("\"name\"") - 3;
                data = t.substring(start, end);

                t = t.substring(end + 1);
                start = t.indexOf(":") + 3;
                end = t.indexOf("}") - 1;
                name = t.substring(start, end);

                l[j - 1] = new locations(id, lat, lng, data, name);

            }
        } else {
            l = new locations[0];
        }
        return l;
    }


    //     <!--   Get Live location with permission
    private static int REQUEST_LOCATION_PERMISSION = 1;

    private boolean isPermissionGranted() {
        return ContextCompat.checkSelfPermission(
                this.requireContext(),
                Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED;
    }

    private void enableMyLocation() {
        if (isPermissionGranted()) {
            map.setMyLocationEnabled(true);

        }
        else {
            ActivityCompat.requestPermissions(
                    this.requireActivity(),
                    new String[]{(Manifest.permission.ACCESS_FINE_LOCATION)},
                    REQUEST_LOCATION_PERMISSION
            );
        }
    }


    private GoogleMap  map;

//    Get Live location with permission >>

    private LocationViewModel mViewModel;

    public static location newInstance() {
        return new location();
    }

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.location_fragment, container, false);
        SupportMapFragment mMapFragment = SupportMapFragment.newInstance();
        FragmentTransaction fragmentTransaction =
                getChildFragmentManager().beginTransaction();
        fragmentTransaction.add(R.id.map, mMapFragment);
        fragmentTransaction.commit();
        mMapFragment.getMapAsync(this);

        return view;
    }

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        mViewModel = ViewModelProviders.of(this).get(LocationViewModel.class);
        // TODO: Use the ViewModel
    }

    @Override
    public boolean onMarkerClick(Marker marker) {
        locations mar = (locations)marker.getTag();

//        Snackbar.make(getView(), "id for this is "+mar.id, Snackbar.LENGTH_LONG)
//                .setAction("Action", null).show();

        Toast.makeText(this.getActivity(),"For direction ",Toast.LENGTH_SHORT).show();

        Intent i = new Intent(getActivity().getApplicationContext(), PopActivity.class);
        i.putExtra("id",""+mar.id);
        i.putExtra("name",""+mar.name);
        i.putExtra("s",""+mar.s);

        startActivity(i);
        return false;
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        map = googleMap;
        map.getUiSettings().setMapToolbarEnabled(true);

        googleMap.setOnMarkerClickListener(this);
        Toast.makeText(this.getActivity(),"Wait while station locations are searching",Toast.LENGTH_LONG).show();
        Log.d("result", "onMapReady: before_connection");
//----------------------------------------

        GetMarkers myTask = new GetMarkers();
        myTask.m = map;
        myTask.execute("");

//------------------------------------

        enableMyLocation();
    }
}
