package cn.edu.tsinghua.thss.popcorn;

import android.app.ListActivity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.beardedhen.androidbootstrap.FontAwesomeText;
import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import cn.edu.tsinghua.thss.popcorn.config.Config;

public class RecordListActivity extends ListActivity {

    private List<Map<String, Object>> mData;

    private String[] mBrief, mFormContent;

    private TableListAdapter mAdapter;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //String[] str_title = {"设备一","设备二","设备三","设备四","设备五"};
        Bundle tmp_bundle = this.getIntent().getExtras();
        String route_id = tmp_bundle.getString("route_id");

        String ROUTE_GET_URL = Config.LOCAL_IP + "/app/form";
        mAdapter = new TableListAdapter(this);

        RequestParams params = new RequestParams();
        params.addQueryStringParameter("route_id", String.valueOf(route_id));


        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String time = df.format(new Date());
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);
        params.addQueryStringParameter("timestamp", time);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                ROUTE_GET_URL,
                params,
                new RequestCallBack<String>() {

                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");
                            ArrayList<String> tmp_title = new ArrayList<String>();
                            ArrayList<String> tmp_form_content = new ArrayList<String>();
                            if (status.equals("ok")) {
                                JSONArray results = jsonObject.getJSONArray("data");
                                for (int i = 0; i < results.length(); ++i) {
                                    JSONObject result = results.getJSONObject(i);
                                    String name = result.getString("name");
                                    String form_content = result.getString("form_content");
                                    tmp_title.add(name);
                                    tmp_form_content.add(form_content);
                                }
                                mBrief = tmp_title.toArray(new String[]{});
                                mFormContent = tmp_form_content.toArray(new String[]{});
                                mData = getData(mBrief);
                                //TableListAdapter adapter = new TableListAdapter(this);
                                setListAdapter(mAdapter);
                            } else {
                                Toast.makeText(getApplicationContext(), "该路线未设置设备", Toast.LENGTH_SHORT).show();
                                //bottomTabMeterText.setText(String.valueOf(1));
                                //bottomTabMeterText.setText("2");
                                //bottomTabMeterText.setTextSize(50);
                                //bottomTabMeterText.setVisibility(View.GONE);
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), error.getExceptionCode() + ":" + msg, Toast.LENGTH_SHORT).show();
                    }
                });
    }

    @Override
    public void onListItemClick(ListView l, View v, int position, long id) {
        Intent intent=new Intent(this, TableActivity.class);
        Bundle bundle=new Bundle();
        bundle.putString("form_content", mFormContent[(int)id]);
        intent.putExtras(bundle);
        startActivity(intent);

        super.onListItemClick(l, v, position, id);
    }


    private List<Map<String, Object>> getData(String[] str_title) {
        List<Map<String ,Object>> list = new ArrayList<Map<String,Object>>();

        for (int i = 0; i < str_title.length; i++) {
            Map<String, Object> map = new HashMap<String, Object>();
            map.put("title", str_title[i]);
            list.add(map);
        }

        return list;
    }

    class ViewHolder {
        public TextView title;
        public FontAwesomeText faText;
    }

    public class TableListAdapter extends BaseAdapter {
        private LayoutInflater mInflater = null;

        public TableListAdapter(Context context) {
            super();
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }

        @Override
        public int getCount() {
            return mData.size();
        }

        @Override
        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {

            ViewHolder holder = null;
            if (convertView == null) {
                holder = new ViewHolder();
                convertView = mInflater.inflate(R.layout.listview_record, null);
                holder.title = (TextView) convertView.findViewById(R.id.title);
                holder.faText = (FontAwesomeText) convertView.findViewById(R.id.front_icon);
                convertView.setTag(holder);
            } else {
                holder = (ViewHolder) convertView.getTag();
            }

            holder.title.setText((String)mData.get(position).get("title"));
           if(position == 1) {
               holder.faText.setTextColor(Color.parseColor("#D3D3D3"));
           }
           return convertView;
        }
    }



    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.record, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            RecordListActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}